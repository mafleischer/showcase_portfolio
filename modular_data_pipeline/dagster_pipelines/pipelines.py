from dagster import job, op
from plugins.github_plugin import GitHubPlugin
from plugins.csv_plugin import CSVPlugin
from models import PipelineLog, Session


@op(config_schema={"plugin": str})
def fetch_data_op(context):
    plugin_name = context.op_config["plugin"]
    plugin_class = GitHubPlugin if plugin_name == "github" else CSVPlugin
    plugin = plugin_class()
    data = plugin.fetch_data()

    session = Session()
    log = PipelineLog(plugin_name=plugin_name, result_data=data)
    session.add(log)
    session.commit()

    return data


@op
def print_data_op(data: dict):
    print("Fetched Data:", data)


@job(config={"ops": {"fetch_data_op": {"config": {"plugin": "github"}}}})
def data_pipeline():
    print_data_op(fetch_data_op())
