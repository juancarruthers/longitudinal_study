from GithubGraphQL import GithubGraphQL as GQL
import subprocess
from XiaFilter import *

def retrieveProjects(queryFilter: str, secondFilter: dict, folderPath: str, savethreshold = 5000, p_itemsPageMainQuery = 30):

    if not (os.path.isdir(folderPath)):
        os.mkdir(folderPath)

    projectRetriever = GQL(queryFilter, secondFilter, folderPath, p_saveThreshold=savethreshold, p_itemsPageMainQuery=p_itemsPageMainQuery)
    projectRetriever.main()

def xiaMonthlyData(xiaCodePath: str, projectListPath: str):

    if not (os.path.isdir(f'{xiaCodePath}/experiment/data')):
        os.mkdir(f'{xiaCodePath}/experiment/data')
        with open('problem_repo.txt', 'w'):
            pass

    dataset = pd.read_csv(f"{projectListPath}/retrieved-projects.csv")
    dataset['url'].to_csv(f"{xiaCodePath}/experiment/data/repo_list.csv", index=False, header=False)
    command = [f'{xiaCodePath}/venv/Scripts/python.exe', 'master_runner.py']
    subprocess.run(command, cwd=f'{xiaCodePath}/experiment')

def generateLongStudyDatasets(xiaCodePath: str, projectListPath: str):
    dataset = pd.read_csv(f"{projectListPath}/retrieved-projects.csv")
    dataset[['id', 'url', 'createdAt']].to_csv(f"{xiaCodePath}/experiment/monthly_results/allProjects.csv", index=False)
    fixErrorsXiaMonthlyData(xiaCodePath)

    xiaFilters = {'commits': 1000, 'pullReqCount': 50, 'closedIssuesCount': 50, 'contributors': 3, 'forkCount': 10,
                  'stargazerCount': 10, 'activity': {'months': 1, 'active': True}, 'age': {'years': 1, 'active': True}}

    # RQ1 and RQ2 data
    framesData = f'{projectListPath}/snapshots'
    generateDataset(xiaFilters, '2017-07-01', '2023-06-01', xiaCodePath, framesData)

    print(f"{dataset.shape[0]} Projects retrieved initially")

    # Discard projects not included in any snapshot
    completeDataset = pd.DataFrame()
    for subdir, dirs, files in os.walk(framesData):
        for dir in dirs:
            frame = pd.read_csv(f"{framesData}/{dir}/frame.csv").copy()
            frame['waves'] = dir
            completeDataset = pd.concat([completeDataset, frame])
    completeDataset = completeDataset.drop_duplicates(subset=['id'])

    dataset[dataset['id'].isin(completeDataset['id'])].to_csv(f"{projectListPath}/final-list.csv", index=False)
    print(f"{completeDataset.shape[0]} Projects kept")
    deletedProjects = dataset[~dataset['id'].isin(completeDataset['id'])]
    discardProjects(xiaCodePath, deletedProjects)

    # RQ3 data
    xiaFilters = {'commits': 0, 'pullReqCount': 0, 'closedIssuesCount': 0, 'contributors': 0, 'forkCount': 0,
                  'stargazerCount': 0, 'activity': {'months': 1, 'active': True}, 'age': {'years': 1, 'active': False}}

    updatesData = f'{projectListPath}/updates-monthly-data'
    generateDataset(xiaFilters, '2009-01-01', '2023-06-01', xiaCodePath, updatesData)

if __name__ == '__main__':

    JUNE_1ST_2022 = '2022-06-01'
    PROJ_RETRIEVAL_PATH = "./dataset"
    XIA_CODE_PATH = './Health_Indicator_Prediction'

    QUERY_FILTER = f"is:public, language:java, mirror:false, forks:>=10, stars:>=10, created:<={JUNE_1ST_2022}"
    SECOND_FILTER = {'keywords': ['sample', 'tutorial', 'demo', 'conf', 'exam', 'docs', 'benchmark', 'wiki'], 'totalSize': 10000, 'commits': 1000,
                    'closedIssuesCount': 50, 'pullReqCount': 50 , 'dateLastActivity': '1970-01-01', 'contributors': 3}


    retrieveProjects(QUERY_FILTER, SECOND_FILTER, PROJ_RETRIEVAL_PATH)
    xiaMonthlyData(XIA_CODE_PATH, PROJ_RETRIEVAL_PATH)
    generateLongStudyDatasets(XIA_CODE_PATH, PROJ_RETRIEVAL_PATH)













