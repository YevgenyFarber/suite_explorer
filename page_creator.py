from xhtml_cleaner import saved_char_replacement


class Page:
    def __init__(self, suite_name: str, suite_data: dict) -> None:
        self.suite_name = suite_name
        self.suite_data = suite_data

    def create_page(self) -> str:
        sections_html = f'<h2>{self.suite_name}</h2>'
        for feature_name, suite_data in self.suite_data.items():
            sections_html += f'<h3>{feature_name}</h3>'
            for suite_name, suite_content in suite_data.items():
                sections_html += f'<h4>{suite_name}</h4>'
            # Extracting data for each suite
                test_names = suite_content.get('test_name', [])
                owners = suite_content.get('owners', '')
                path = suite_content.get('path', '')

                tests_html = ''.join(
                    f"<li><p><code>{saved_char_replacement(test)}</code></p></li>"
                    for test in test_names
                )
                owners_html = ''.join(
                    f'<p><ac:link><ri:user ri:account-id=\"{owner}\" /></ac:link></p>'
                    for owner in owners
                )
                # Generating a section for each suite
                section_html = f"""
                <table data-table-width="1240" data-layout="default">
                  <colgroup>
                    <col style="width: 663.0px;" />
                    <col style="width: 183.0px;" />
                    <col style="width: 220.0px;" />
                  </colgroup>
                  <tbody>
                    <tr>
                      <th><p><strong>Tests</strong></p></th>
                      <th><p><strong>Cycle</strong></p></th>
                      <th><p><strong>Owner</strong></p></th>
                    </tr>
                    <tr>
                      <td><ul>{tests_html}</ul></td>
                      <td><p>{path}</p></td>
                      <td>{owners_html}</td>
                    </tr>
                  </tbody>
                </table>
                """
                sections_html += section_html

        # Creating the final HTML content
        return sections_html
