from nptel import Nptel as npt


if __name__ == '__main__':

    dept_key = 'CSE'
    dept = npt.get_departments()[dept_key]
    branchID = dept['branchID']
    cid = dept['cid']

    subjects = npt.get_subjects(branchID=branchID,
                                  cid=cid)

    for subject in subjects:
        topics = npt.get_topics(value=subject['value'],
                                  branchID=branchID,
                                  cid=cid)

        for topic in topics:
            sub_topics = npt.get_sub_topics(topic=topic,
                                              value=subject['value'],
                                              branchID=branchID,
                                              cid=cid)
            print(topic, sub_topics)
