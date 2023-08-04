import pandas as pd
from datetime import datetime
from Filters.__init__ import *
import os
import shutil

def fixErrorsXiaMonthlyData(xiaPath: str):
    origin_path = f'{xiaPath}/experiment/monthly_results'

    for subdir, dirs, files in os.walk(origin_path):
        for dir in dirs:
            path = f'{origin_path}/{dir}'
            filesInDirectory = os.listdir(path)
            if len(filesInDirectory) < 5:
                shutil.rmtree(path)

def discardProjects(xiaPath: str, discardedProjects: pd.DataFrame):
    origin_path = f'{xiaPath}/experiment/monthly_results'

    for id, project in discardedProjects.iterrows():
        path = f'{origin_path}/{project["owner"]}-{project["name"]}'
        if (os.path.exists(path)):
            os.remove(f'{path}_monthly.csv')
            shutil.rmtree(path)


#Dates in format yyyy-mm-dd
def generateDataset(thresholds: dict, startDate: str, endDate: str, xiaPath: str, outputFolder: str):
    months = pd.date_range(startDate, endDate, freq="MS")
    origin_path = f'{xiaPath}/experiment/monthly_results'
    filters = _setFilters(thresholds)
    if (not os.path.exists(outputFolder)):
        os.mkdir(outputFolder)

    for month in months:
        month_data = pd.DataFrame()
        date: datetime = month

        for subdir, dirs, files in os.walk(origin_path):
            for dir in dirs:
                path = f'{origin_path}/{dir}'
                filesInDirectory = os.listdir(path)
                fileIndex = [index for index, element in enumerate(filesInDirectory) if '_commits_and_comments.csv' in element][0]
                name = os.listdir(path)[fileIndex].replace('_commits_and_comments.csv', "")
                pos = dir.rfind(f'-{name}')
                owner = dir[:pos]
                url = f'https://github.com/{owner}/{name}'
                row = pd.DataFrame(
                    {'id': [''], 'url': [url], 'owner': [owner], 'name': [name], 'createdAt': [0], 'commits': [0],
                     'dateLastCommit': [0], 'contributors': [0], 'closedPullReqCount': [0],
                     'closedPullReqLastDate': [0], 'mergedPullReqCount': [0], 'mergedPullReqLastDate': [0],
                     'stargazerCount': [0], 'forkCount': [0], 'closedIssuesCount': [0], 'monthlyclosedPullReq': [0],
                     'monthlyCommits': [0], 'monthlymergedPullReq': [0]})
                filtersFlag = False

                for filter in filters:
                    filtersFlag = filter.xiaUpdateFrame(row, f'{path}/{name}', date)
                    if filtersFlag:
                        break
                if not filtersFlag:
                    month_data = pd.concat([month_data, row], axis=0)
                    print(f'Added {url} in month {month}')

        destination_path = f'{outputFolder}/{str(month.strftime("%Y-%m-%d"))}'
        if (not os.path.exists(destination_path)):
            os.mkdir(destination_path)

        month_data.to_csv(f'{destination_path}/frame.csv', index=False)

def _setFilters(thresholds: dict) -> list[GraphqlFilter]:

    filters = ['commits', 'pullReqCount', 'closedIssuesCount', 'contributors', 'forkCount', 'stargazerCount', 'activity', 'age']
    filtersConfig = []
    for filter in filters:
        filterConfig = GraphqlFilter
        if filter in thresholds:
            if filter == 'commits':
                filterConfig = CommitFilter({filter: thresholds[filter]})
            if filter == 'closedIssuesCount':
                filterConfig = IssuesFilter({filter: thresholds[filter]})
            if filter == 'pullReqCount':
                filterConfig = PullReqFilter({filter: thresholds[filter]})
            if filter == 'contributors':
                filterConfig = ContributorsFilter({filter: thresholds[filter]})
            if filter == 'forkCount':
                filterConfig = ForkFilter({filter: thresholds[filter]})
            if filter == 'stargazerCount':
                filterConfig = StargazerFilter({filter: thresholds[filter]})
            if filter == 'activity':
                filterConfig = RecentActivityFilter({filter: thresholds[filter]})
            if filter == 'age':
                filterConfig = AgeFilter({filter: thresholds[filter]})

            filtersConfig.append(filterConfig)
        else:
            print(f"{filter} filter not set")
            exit()

    return filtersConfig