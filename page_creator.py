from xhtml_cleaner import saved_char_replacement


class Page:
    def __init__(self, suite_name, suite_data):
        self.suite_name = suite_name
        self.suite_data = suite_data

    def create_page(self):
        sections_html = f'<h2>{self.suite_name}</h2>'
        for feature_name, suite_data in self.suite_data.items():
            sections_html += f'<h3>{feature_name}</h3>'
            for suite_name, suite_content in suite_data.items():
                print()
            # Extracting data for each suite
                test_names = suite_content.get('test_name', [])
                owners = suite_content.get('owners', '')
                path = suite_content.get('path', '')

                # Generating HTML for tests
                tests_html = ''
                for test in test_names:
                    tests_html += f"<li><p><code>{saved_char_replacement(test)}</code></p></li>"
                    # tests_html += f"<li><p><code>{test}</code></p></li>"

                # Generating HTML for owners (assuming owners are a single string or a list of strings)
                owners_html = ''
                for owner in owners:
                    owners_html += f"<p><ac:link><ri:user ri:account-id=\"{owner}\" /></ac:link></p>"

                # Generating a section for each suite
                section_html = f"""
                <table data-table-width="1240" data-layout="default">
                  <colgroup>
                    <col style="width: 663.0px;" />
                    <col style="width: 170.0px;" />
                    <col style="width: 183.0px;" />
                    <col style="width: 220.0px;" />
                  </colgroup>
                  <tbody>
                    <tr>
                      <th><p><strong>Tests</strong></p></th>
                      <th><p><strong>Suite name</strong></p></th>
                      <th><p><strong>Cycle</strong></p></th>
                      <th><p><strong>Owner</strong></p></th>
                    </tr>
                    <tr>
                      <td><ul>{tests_html}</ul></td>
                      <td><p>{suite_name}</p></td>
                      <td><p>{path}</p></td>
                      <td>{owners_html}</td>
                    </tr>
                  </tbody>
                </table>
                """
                sections_html += section_html

        # Creating the final HTML content
        return sections_html
