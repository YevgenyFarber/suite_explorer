def get_page_actions(client):
    # page = self.clients.confluence.get_page_id('AT1', 'Test NET60 IP Pool')
    # page = self.clients.confluence.get_page_properties('72220910')
    page = client.get_page_by_title('RnD', 'YevgenyTesting', expand='body.storage')
    # page = self.clients.confluence.get_page_by_title('SWR', 'report 17.50', expand='body.storage')
    # page = self.clients.confluence.get_page_by_id('74122368', expand='version')
    # page = self.clients.confluence.get_all_spaces()
    # page = self.clients.confluence.get_space('SWSAN', expand='description.plain,homepage')
    print(page)
    print()


def update_page(client, page_id, title, body):
    client.update_or_create(
        page_id, title, body, representation='storage', editor='v2')
