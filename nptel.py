from request import Request


request = Request(base_url='https://gate.nptel.ac.in').request


class Nptel:

    def get_departments():

        soup = request(method='GET',
                       endpoint='departments.php',
                       params={'c_id': 1})

        return {
            tag.img['alt']: {
                'branchID': end_pt[0].split('=')[1],
                'cid': end_pt[1].split('=')[1]
            } for tag in soup.find_all('div', {'class': 'card'})
            if (end_pt := tag.a['href'].split('?')[1].split('&'))}

    # ------------------------------------------------------------------

    def get_subjects(branchID,
                     cid):

        soup = request(method='GET',
                       endpoint='video.php',
                       params={'branchID': branchID,
                               'cid': cid})

        return [{
            'subject': tag.text,
            'value': tag['value'],
        } for tag in soup.find_all('option') if tag['value']]

    # ------------------------------------------------------------------

    def get_topics(value,
                   branchID,
                   cid):

        return request(method='POST',
                       endpoint='listvideos.php',
                       data={'inputValue': value,
                             'branchID': branchID,
                             'cid': cid},
                       is_json=True)

    # ------------------------------------------------------------------

    def get_sub_topics(topic,
                       value,
                       branchID,
                       cid):

        soup = request(method='POST',
                       endpoint='listvideos.php',
                       data={'keyword': topic,
                             'Topics': value,
                             'branchID': branchID,
                             'cid': cid})

        content = []  # this part needs refactoring
        for td in soup.find_all('td'):
            if td.get('id') == 'bold':
                key = td.text
                content.append({key: []})
            elif td.text:
                content[-1][key].append({'topic': td.text})
            else:
                _id = td.a["href"].split("('")[1].split("')")[0]
                content[-1][key][-1]['url']=f'https://www.youtube.com/watch?v={_id}'

        return content

    # ------------------------------------------------------------------
