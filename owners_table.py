class OwnersTable:
    @staticmethod
    def static_table():
        return '<table class="default"> \
                    <colgroup> \
                        <col style="width: 340.0px;" /> \
                        <col style="width: 340.0px;" /> \
                    </colgroup> \
                    <tbody> \
                        <tr> \
                            <th>Owner</th> \
                            <th>Suite Count</th> \
                        </tr>'

    @staticmethod
    def row_creator(owner, count):
        return (f'<tr><td><p><ac:link><ri:user ri:account-id=\"{owner}\" '
                f'/></ac:link></p></td><td><span style="color: rgb(51,51,51);">{count}</span></td></tr>')

    @staticmethod
    def end_of_table():
        return '</tbody></table>'
