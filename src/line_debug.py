def reply(reply_token: str, message: str):
    print(f'line_debug: {reply_token=} {message=}')


def multicast(message: str, user_ids: list[str]):
    print(f'line_debug: {message=} {user_ids=}')
