from atlassian import Confluence


def confluence_connection(user_name, password):

    return Confluence(
        url='https://catonetworks.atlassian.net/',
        username=user_name,
        password=password,
        timeout=580,
        verify_ssl=False
    )

