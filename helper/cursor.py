def spinning_cursor():
    """
    Generator for a spinning cursor animation.

    :return: Yields the next character in the spinning cursor sequence.
    """
    while True:
        for cursor in '|/-\\':
            yield cursor