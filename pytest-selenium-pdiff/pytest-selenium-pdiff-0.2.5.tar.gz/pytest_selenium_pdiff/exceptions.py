class MissingScreenshot(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, *args, **kwargs):
        message = 'Cannot find the screenshot named ' \
                  '"{}" at {}, screenshot capture is disabled.'

        message = message.format(screenshot_name,
                                 screenshot_path
                                 )

        super(MissingScreenshot, self).__init__(message, *args, **kwargs)


class ScreenshotMismatch(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, pdiff_output, *args, **kwargs):
        message = 'Captured screenshot named "{}", does not match stored ' \
                  'screenshot "{}", perceptualdiff returned: "{}".  '

        message = message.format(
            screenshot_name,
            screenshot_path,
            pdiff_output
        )

        super(ScreenshotMismatch, self).__init__(message, *args, **kwargs)


class ScreenshotMismatchWithDiff(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, diff_path, pdiff_output, *args, **kwargs):
        message = 'Captured screenshot named "{}", does not match stored screenshot "{}".  ' \
                  'Diff is available at: "{}", perceptualdiff returned: {}.'

        message = message.format(
            screenshot_name,
            screenshot_path,
            diff_path,
            pdiff_output
        )

        super(ScreenshotMismatchWithDiff, self).__init__(message, *args, **kwargs)
