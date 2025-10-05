from kaggle.api.kaggle_api_extended import KaggleApi
def search_datasets(keyword):
    api = KaggleApi()
    api.authenticate()
    # Search for datasets matching the keyword
    datasets = api.dataset_list(search=keyword)
    results = []
    for ds in datasets:
        # ds.title is the human name, ds.ref is "owner/dataset-slug"
        results.append((ds.title, ds.ref))
    return results