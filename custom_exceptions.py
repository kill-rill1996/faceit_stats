
class PlayerInfoException(Exception):
    """Raised when function cant get player info from faceit server"""

    def __init__(self, nickname: str, server_errors):
        self.message = f'Failed to get information about player {nickname}.\nServer error {server_errors}'
        super().__init__(self.message)
