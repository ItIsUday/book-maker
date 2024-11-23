from pypdf import PdfReader


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

def rotate_pages(interleaved_pages, degrees):
    pass


def merge_pages(rotated_pages):
    pass


def main():
    reader = PdfReader()
    pages = reader.pages
    partition1, partition2 = equal_partition(pages)
    interleaved_pages = interleave(partition2, partition1)
    rotated_pages = rotate_pages(interleaved_pages, 90)
    merged_pages = merge_pages(rotated_pages)


if __name__ == '__main__':
    main()
