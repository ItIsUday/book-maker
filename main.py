from pypdf import PdfReader


def equal_partition(pages):
    pass


def interleave(partition2, partition1):
    pass


def rotate_pages(interleaved_pages, degrees):
    pass


def merge_pages(rotated_pages):
    pass


def main():
    reader = PdfReader()
    pages = reader.pages
    partition1, partition2 = equal_partition(pages)
    reversed_partition2 = reversed(partition2)
    interleaved_pages = interleave(reversed_partition2, partition1)
    rotated_pages = rotate_pages(interleaved_pages, 90)
    merged_pages = merge_pages(rotated_pages)


if __name__ == '__main__':
    main()
