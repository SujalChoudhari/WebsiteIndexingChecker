class ProgressManager:
    progress = "All Systems Running"
    is_working = "False"

    @staticmethod
    def update_progress(text, is_working=True):
        ProgressManager.progress = text
        ProgressManager.is_working = "True" if is_working else "False"
