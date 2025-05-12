from agents.tasks import handle_task

class SpotnxtAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def respond(self, message: str) -> str:
        # Decide what task to perform based on user input
        response = await handle_task(message, self.user_id)
        return response
