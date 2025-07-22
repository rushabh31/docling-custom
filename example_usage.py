import logging
import os
from pathlib import Path
import datetime
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.datamodel.pipeline_options_vlm_model import ResponseFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from groq_api import groq_vlm_options
from docling.utils.export import generate_multimodal_pages
from docling.utils.utils import create_hash
from template_utils import render_prompt_template

def main():
    """Example showing how to use Groq API with docling document processing."""
    logging.basicConfig(level=logging.INFO)
    load_dotenv()  # Load environment variables from .env file

    # Verify API key is available
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable not set. Please set it in your .env file")
        return

    # Set up the document path
    data_folder = Path(__file__).parent
    input_doc_path = data_folder / "embedded-images-tables.pdf"
    if not input_doc_path.exists():
        print(f"Error: Input document not found at {input_doc_path}")
        return

    # Configure pipeline options with Groq
    pipeline_options = VlmPipelineOptions(
        enable_remote_services=True  # Required for remote API calls
    )

    pipeline_options.images_scale = 2.0
    pipeline_options.generate_page_images = True

    # Load and render prompt template
    template_path = Path(__file__).parent / "templates" / "ocr_prompt.jinja"
    
    # Render the template with context
    rendered_prompt = render_prompt_template(
        str(template_path),
        context={
            "summarize_visuals": True,
            "include_page_number": True
        },
        is_file=True
    )
    
    # Configure Groq API options with the rendered template
    pipeline_options.vlm_options = groq_vlm_options(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # or another Groq model with vision capabilities
        prompt=rendered_prompt,
        format=ResponseFormat.MARKDOWN,
    )

    # Create the document converter and process the document
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=VlmPipeline,
            )
        }
    )
    
    # Run the conversion
    result = doc_converter.convert(input_doc_path)
    print(result.document.export_to_markdown())
    # conv_res = doc_converter.convert(input_doc_path)
    # output_dir = Path("scratch")
    # output_dir.mkdir(parents=True, exist_ok=True)
    # start_time = time.time()
    # rows = []
    # for (
    #     content_text,
    #     content_md,
    #     content_dt,
    #     page_cells,
    #     page_segments,
    #     page,
    # ) in generate_multimodal_pages(conv_res):
    #     dpi = page._default_image_scale * 72

    #     rows.append(
    #         {
    #             "document": conv_res.input.file.name,
    #             "hash": conv_res.input.document_hash,
    #             "page_hash": create_hash(
    #                 conv_res.input.document_hash + ":" + str(page.page_no - 1)
    #             ),
    #             "image": {
    #                 "width": page.image.width,
    #                 "height": page.image.height,
    #                 "bytes": page.image.tobytes(),
    #             },
    #             "cells": page_cells,
    #             "contents": content_text,
    #             "contents_md": content_md,
    #             "contents_dt": content_dt,
    #             "segments": page_segments,
    #             "extra": {
    #                 "page_num": page.page_no + 1,
    #                 "width_in_points": page.size.width,
    #                 "height_in_points": page.size.height,
    #                 "dpi": dpi,
    #             },
    #         }
    #     )

    # # Generate one parquet from all documents
    # df_result = pd.json_normalize(rows)
    # now = datetime.datetime.now()
    # output_filename = output_dir / f"multimodal_{now:%Y-%m-%d_%H%M%S}.parquet"
    # df_result.to_parquet(output_filename)

    # end_time = time.time() - start_time


if __name__ == "__main__":
    main()
