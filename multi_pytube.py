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
                                   split(' ') if p]) for path in path_list])

    def __get_path_url(self, path_list):
        path = self.__path_creater(path_list[:-2])
        return path, path_list[-1]

    def get_subjects_path_url(self):
        for sub in self.df['SUBJECT'].unique():
            subject_df = self.df.loc[lambda x: x['SUBJECT'] == sub]
            subject_df.insert(0, 'BASE_DIR', self.base_dir)
            yield list(map(self.__get_path_url, subject_df.values))

    @staticmethod
    def __multi_download(path, url):
        YoutubeDL({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s'

        }).download(url)

    def start_downloader(self, path_url_list):
        process_list = [Process(target=self.__multi_download,
                                args=(path, url,))
                        for path, url in tqdm(path_url_list,
                                              desc='Creating Process')]
        [proc.start() for proc in tqdm(process_list, desc='Starting Process')]
        [proc.join() for proc in tqdm(process_list, desc='Joining Process')]
        print('Download Completed')
