def get_page_actions(client):
    # page = self.clients.confluence.get_page_id('AT1', 'Test NET60 IP Pool')
    # page = self.clients.confluence.get_page_id('SWR', 'RIUD Regression view')
    # page = client.get_page_id('RnD', 'Security inline tests')
    # page = self.clients.confluence.get_page_properties('72220910')
    page = client.get_page_by_title('RnD', 'Security inline tests',
                                    expand='body.storage')  # page = self.clients.confluence.get_page_by_title(
    #         'SWR', 'SR18.50 5G Executive View Dashboard',
    #         expand='body.storage')
    # page = self.clients.confluence.get_page_by_title(
    #         'SWR', 'Build 18.00.1309 - Core Occurrence count', expand='body.storage')
    # page = self.clients.confluence.get_page_by_title('SWR', 'report 17.50', expand='body.storage')
    # page = self.clients.confluence.get_page_by_title('SWR', 'Rakuten_17.00.639', expand='body.storage')
    # page = self.clients.confluence.get_page_by_title('SWR', '17.50.630', expand='version')
    # page = self.clients.confluence.get_page_by_id('74122368', expand='version')
    # page = self.clients.confluence.get_all_spaces()
    # page = self.clients.confluence.get_space('SWSAN', expand='description.plain,homepage')
    # print(page.values())
    # x = list(page.version.values())
    # x = page.get('version', {}).get('number')
    print(page)
    print()


def update_page(client, page_id, title, body):
    client.update_or_create(
        page_id, title, body, representation='storage', editor='v2')


