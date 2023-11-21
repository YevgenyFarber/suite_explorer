from atlassian import Confluence

from page_actions import get_page_actions, update_page


def confluence_connection(user_name, password):

    return Confluence(
        # url='https://confluence.airspan.com/',
        # url='http://confluence-internal:8090/',
        url='https://catonetworks.atlassian.net/',
        username=user_name,
        password=password,
        timeout=580,
        verify_ssl=False
    )



if __name__ == '__main__':
    client = confluence_connection('yevgeny.farber@catonetworks.com', 'ATATT3xFfGF0VLt_CaxpIUEk2GmbWbAdOY650omxMFAicxRJ6KokUUQ-lwY4P5u3M7MGwLexB7wRQzi4ntgIgJwPX-tPMtLrVk88bVDqbLdP8oMQWb8rgut23E1WEEIXGqpay80L9iN33Q1tBeHFCKIQWT-etTMKqBFCDQ0FLPdSVCbXm0mVt0A=1009B3C6')

    users = client.get_user_details_by_accountid('606b098296e8d60068ac4ab1')

    get_page_actions(client)
    with open('confluence_template.txt') as template_file:
        update_page(client, '2780823557', 'YevgenyTesting', template_file.read())
        print()
    x = get_page_actions(client)
