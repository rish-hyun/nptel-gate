from nptel import Nptel as npt
from multi_yt_dlp import MultiYtDlp
import pandas as pd


def create_csv(dept_key):

    dept = npt.get_departments()
    branchID = dept[dept_key]['branchID']
    cid = dept[dept_key]['cid']

    subjects = npt.get_subjects(branchID=branchID, cid=cid)

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
                        data.append({'SUBJECT': subject['subject'],
                                     'TOPIC': topic,
                                     'SUB TOPIC 1': sub_topic_1,
                                     'SUB TOPIC 2': sub_topic_2['topic'],
                                     'URL': sub_topic_2['url']})

    df = pd.DataFrame(data)
    df.to_csv(f'{dept_key}.csv', index=False)
    return df


if __name__ == '__main__':

    dept_key = 'CSE'
    base_dir = f'/content/drive/MyDrive/{dept_key}'

    df = create_csv(dept_key=dept_key)
    # df = pd.read_csv(f'{dept_key}.csv', index_col=None)

    myd = MultiYtDlp(src_df=df, base_dir=base_dir)
    for path_url in myd.get_subjects_path_url():
        myd.start_downloader(path_url)
