import argparse
from itertools import chain

from more_itertools import divide
from pypdf import PdfReader, PdfWriter, PageObject


def merge_pages(partitions):
    # TODO: Move from for loop to map.
    for i, (page1, page2) in enumerate(zip(*partitions)):
        page_width, page_height = page1.mediabox.width, page1.mediabox.height
        page1, page2 = (page1, page2) if i % 2 else (page2, page1)

        new_page = PageObject.create_blank_page(
            height=page_height, width=page_width * 2)
        new_page.merge_translated_page(page1, page_width, 0)
        new_page.merge_translated_page(page2, 0, 0)
        new_page.scale_by(0.5)

        yield new_page


def read_pages(filename, make_even=True):
    pdf_reader = PdfReader(filename)
    padding_pages = (
        [PageObject.create_blank_page(pdf_reader)]
        if make_even and len(pdf_reader.pages) % 2
        else []
    )
    return chain(pdf_reader.pages, padding_pages)


def write_pages(filename, pages):
    pdf_writer = PdfWriter()
    # TODO: Get rid of an explicit for loop.
    for page in pages:
        pdf_writer.add_page(page)

    with open(filename, "wb") as output_file:
        pdf_writer.write(output_file)


def parse_arguments():
    parser = argparse.ArgumentParser(prog="Book Maker",
                                     description="Converts PDF into books for easy printing")
    parser.add_argument("input_pdf",
                        type=str,
                        help="Input PDF filepath"
                        )
    parser.add_argument("-o",
                        "--output_pdf",
                        type=str,
                        help="Output PDF filepath",
                        default="output.pdf"
                        )
    args = parser.parse_args()
    return args.input_pdf, args.output_pdf


def main():
    # TODO: Use function composition here.
    input_file, output_file = parse_arguments()
    pages = read_pages(input_file)

    slices = divide(2, pages)
    merged_pages = list(merge_pages(slices))

    # TODO: Get rid of an explicit for loop.
    for i, p in enumerate(merged_pages):
        p.rotate(90 + 180 * (i % 2)).transfer_rotation_to_content()

    write_pages(output_file, merged_pages)


if __name__ == '__main__':
    main()
