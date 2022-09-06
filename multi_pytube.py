from yt_dlp import YoutubeDL
from tqdm import tqdm
from multiprocessing import Process


class MultiPytube:

    def __init__(self, src_df, base_dir):
        self.df = src_df
        self.base_dir = base_dir

    @staticmethod
    def __path_creater(path_list):
        return '/'.join(['_'.join([p for p in path.
                                   replace('-', ' ').
                                   replace(':', ' ').
                                   replace('.', ' ').
                                   replace('\t', ' ').
                                   replace('\n', ' ').
                                   replace('/', '').
                                   split(' ') if p]) for path in path_list])

    def __get_path_url(self, path_list):
        path_list[:0] = [dir for dir in self.base_dir.split('/') if dir]
        path = self.__path_creater(path_list[:-2])
        return path, path_list[-2], path_list[-1]

    def get_subjects_path_url(self):
        for sub in self.df['SUBJECT'].unique():
            subject_df = self.df.loc[lambda x: x['SUBJECT'] == sub]
            yield list(map(self.__get_path_url, subject_df.values))

    @staticmethod
    def __multi_download(path, title, url):
        YoutubeDL({
            'format': 'best',
            'outtmpl': f'{path}/{title}.mp4'
        }).download(url)

    def start_downloader(self, path_url_list):
        process_list = [Process(target=self.__multi_download,
                                args=(path, title, url,))
                        for path, title, url in tqdm(path_url_list,
                                                     desc='Creating Process')]
        [proc.start() for proc in tqdm(process_list, desc='Starting Process')]
        [proc.join() for proc in tqdm(process_list, desc='Joining Process')]
        print('Download Completed')
