from nptel import Nptel as npt
import pandas as pd


if __name__ == '__main__':

    dept_key = 'CSE'

    dept = npt.get_departments()
    branchID = dept[dept_key]['branchID']
    cid = dept[dept_key]['cid']

    subjects = npt.get_subjects(branchID=branchID,
                                cid=cid)

    data = []
    for subject in subjects:
        topics = npt.get_topics(value=subject['value'],
                                branchID=branchID,
                                cid=cid)

        for topic in topics:
            sub_topics = npt.get_sub_topics(topic=topic,
                                            value=subject['value'],
                                            branchID=branchID,
                                            cid=cid)

            for sub_topic in sub_topics:
                for sub_topic_1, sub_topics_2 in sub_topic.items():
                    for sub_topic_2 in sub_topics_2:
                        data.append({'SUBJECT': subject,
                                     'TOPIC': topic,
                                     'SUB TOPIC 1': sub_topic_1,
                                     'SUB TOPIC 2': sub_topic_2['topic'],
                                     'URL': sub_topic_2['url']})

    df = pd.DataFrame(data)
    df.to_csv(f'{dept_key}.csv')
    print(df)
