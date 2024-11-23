from itertools import compress, pairwise, cycle

from pypdf import PdfReader, PdfWriter, PageObject


def equal_partition(pages):
    if len(pages) % 2 != 0:
        width, height = pages[0].mediabox.width, pages[0].mediabox.height
        pages.append(PageObject.create_blank_page(width=width, height=height))
    mid_point = len(pages) // 2

    return pages[:mid_point], pages[mid_point:]


def interleave(partition1, partition2):
    interleaved_pages = list(page for pages in zip(partition1, partition2) for page in pages)

    return interleaved_pages


def rotate_pages(pages, degrees):
    for page in pages:
        page.rotate(degrees)
        page.transfer_rotation_to_content()

    return pages


def merge_pages(pages):
    merged_pages = []
    for i, (page1, page2) in enumerate(compress(pairwise(pages), cycle((1, 0)))):
        page_width, page_height = page1.mediabox.width, page1.mediabox.height
        new_page = PageObject.create_blank_page(None, height=page_width, width=page_height)
        page1.scale_by(page_height / page_width)
        page2.scale_by(page_height / page_width)
        if i % 2 == 0:
            new_page.merge_translated_page(page1, 0, new_page.mediabox.height / 2)
            new_page.merge_page(page2)
        else:
            new_page.merge_translated_page(page2, 0, new_page.mediabox.height / 2)
            new_page.merge_page(page1)
        merged_pages.append(new_page)

    return merged_pages


def write_to_file(pages, filename):
    pdf_writer = PdfWriter()
    for page in pages:
        pdf_writer.add_page(page)
    with open(filename, "wb") as output_file:
        pdf_writer.write(output_file)


def main():
    pdf_filename = "/Users/uarsiker/Downloads/cake.pdf"
    pdf_reader = PdfReader(pdf_filename)
    pages = list(pdf_reader.pages)

    partition1, partition2 = equal_partition(pages)
    interleaved_pages = interleave(partition1, partition2)
    rotated_pages = rotate_pages(interleaved_pages, 90)
    merged_pages = merge_pages(rotated_pages)
    for i in range(1, len(merged_pages), 2):
        merged_pages[i].rotate(180)
    write_to_file(merged_pages, "output.pdf")


if __name__ == '__main__':
    main()

# Design
# 1) Split pages into two equal partition (add a blank if necessary)
# 2) Interleave the first partition with the second partition
# 3) Rotate and Merge every pair of pages
# 4) Flip every odd page
