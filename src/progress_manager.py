class ProgressManager:
    """
        # Progress Manager
        Keeps track of progress and updates the front-end via /api route
    """

    progress = "Working ..."
    is_working = "True"
    done_message = "Process completed!"


    @staticmethod
    def update_progress(text, is_working=True):
        print(text)
        ProgressManager.progress = text
        ProgressManager.is_working = "True" if is_working else "False"
