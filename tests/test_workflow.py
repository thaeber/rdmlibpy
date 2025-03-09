import pandas as pd
import pytest

from rdmlibpy import Workflow, base, loaders, run


def test_run_step(data_path):
    process = {
        'run': 'channel.tclogger@v1',
        'params': {
            'source': data_path / 'ChannelV2TCLog/2024-01-16T11-26-54.csv',
        },
    }
    df = run(process)
    assert isinstance(df, pd.DataFrame)


def test_run_sequence(data_path):
    process = [
        {
            'run': 'channel.tclogger@v1',
            'params': {
                'source': data_path / 'ChannelV2TCLog/2024-01-16T11-26-54.csv',
            },
        },
        {
            'run': 'dataframe.select.columns@v1',
            'params': {
                'select': {
                    "timestamp": "timestamp",
                    "sample-downstream": "temperature",
                },
            },
        },
    ]
    df = run(process)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['timestamp', 'temperature']


class TestProcessNode:
    def test_create_node_with_defaults(self):
        class TestProcess(base.ProcessBase):
            name: str = 'Test'
            version: str = '1'

            def run(self):
                return 'test'

        node = base.ProcessNode(runner=TestProcess())

        assert isinstance(node.runner, TestProcess)
        assert node.parent is None
        assert node.params == {}

    def test_create_node_with_parent(self):
        class TestProcess(base.ProcessBase):
            name: str = 'Test'
            version: str = '1'

            def run(self):
                return 'test'

        parent = base.ProcessNode(runner=TestProcess())
        runner = TestProcess()
        node = base.ProcessNode(runner=runner, parent=parent)

        assert node.runner is runner
        assert node.parent is parent
        assert node.params == {}

    def test_create_node_with_params(self):
        class TestProcess(base.ProcessBase):
            name: str = 'Test'
            version: str = '1'

            def run(self):
                return 'test'

        runner = TestProcess()
        param = base.PlainProcessParam(value='test')
        node = base.ProcessNode(runner=runner, params={'test': param})

        assert node.runner is runner
        assert node.parent is None
        assert len(node.params) == 1
        assert node.params['test'] is param

    def test_create_node_with_str_param(self):
        class TestProcess(base.ProcessBase):
            name: str = 'Test'
            version: str = '1'

            def run(self):
                return 'test'

        runner = TestProcess()
        node = base.ProcessNode(
            runner=runner, params={'test': 'dummy', 'test2': 'dummy2'}  # type: ignore
        )

        assert node.runner is runner
        assert node.parent is None
        assert len(node.params) == 2
        assert isinstance(node.params['test'], base.PlainProcessParam)
        assert node.params['test'].value == 'dummy'
        assert isinstance(node.params['test2'], base.PlainProcessParam)
        assert node.params['test2'].value == 'dummy2'


class TestWorkflow:
    def test_workflow_with_single_process(self, data_path):
        descriptor = {
            'run': 'mks.ftir@v1',
            'params': {
                'source': str(data_path / 'mks_ftir/2024-01-16-conc.prn'),
            },
        }

        # create workflow
        workflow = Workflow.create(descriptor)
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_execute_run_with_params_in_code(self, data_path):
        descriptor = {
            'run': 'mks.ftir@v1',
        }

        # create workflow
        workflow = Workflow.create(descriptor)
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(
            source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'),
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_workflow_with_process_sequence(self, data_path):
        descriptor = [
            {
                'run': 'mks.ftir@v1',
                'params': {
                    'source': str(data_path / 'mks_ftir/2024-01-16-conc.prn'),
                },
            },
            {
                'run': 'dataframe.select.timespan@v1',
                'params': {
                    'column': 'timestamp',
                    'start': '2024-01-16T10:05:22.5',
                    'stop': '2024-01-16T10:05:27.5',
                },
            },
            {
                'run': 'dataframe.select.columns@v1',
                'params': {
                    'select': {
                        "timestamp": "timestamp",
                        "NH3 (3000) 191C (2of2)": "NH3",
                        "N2O (100,200,300) 191C (1of2)": "N2O",
                        "NO (350,3000) 191C": "NO",
                        "NO2 (2000) 191C (2of2)": "NO2",
                        "NO2 (150) 191C (1of2)": "NO2b",
                        "H2O% (25) 191C": "H2O",
                    }
                },
            },
        ]

        # create workflow
        workflow = Workflow.create(descriptor)
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 7

    def test_sequence_of_sequence(self, data_path):
        descriptor = [
            [
                {
                    'run': 'mks.ftir@v1',
                    'params': {
                        'source': str(data_path / 'mks_ftir/2024-01-16-conc.prn'),
                    },
                },
                [
                    {
                        'run': 'dataframe.select.timespan@v1',
                        'params': {
                            'column': 'timestamp',
                            'start': '2024-01-16T10:05:22.5',
                            'stop': '2024-01-16T10:05:27.5',
                        },
                    }
                ],
            ],
            {
                'run': 'dataframe.select.columns@v1',
                'params': {
                    'select': {
                        "timestamp": "timestamp",
                        "NH3 (3000) 191C (2of2)": "NH3",
                        "N2O (100,200,300) 191C (1of2)": "N2O",
                        "NO (350,3000) 191C": "NO",
                        "NO2 (2000) 191C (2of2)": "NO2",
                        "NO2 (150) 191C (1of2)": "NO2b",
                        "H2O% (25) 191C": "H2O",
                    }
                },
            },
        ]

        # create workflow
        workflow = Workflow.create(descriptor)
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 7

    def test_workflow_with_process_params(self, data_path):
        descriptor = [
            {
                'run': 'mks.ftir@v1',
                'params': {
                    'source': str(data_path / 'mks_ftir/2024-01-16-conc.prn'),
                },
            },
            {
                'run': 'dataframe.select.columns@v1',
                'params': {
                    'select': {
                        "timestamp": "timestamp",
                        "NH3 (3000) 191C (2of2)": "NH3",
                        "N2O (100,200,300) 191C (1of2)": "N2O",
                        "NO (350,3000) 191C": "NO",
                        "NO2 (2000) 191C (2of2)": "NO2",
                        "NO2 (150) 191C (1of2)": "NO2b",
                        "H2O% (25) 191C": "H2O",
                    }
                },
            },
            {
                'run': 'dataframe.setindex@v1',
                'params': {
                    'index_var': 'timestamp',
                },
            },
            {
                'run': 'dataframe.join@v1',
                'params': {
                    'interpolate': True,
                    'how': 'left',
                    '$right': [
                        {
                            'run': 'channel.tclogger@v1',
                            'params': {
                                'source': str(
                                    data_path / 'ChannelV2TCLog/2024-01-16T10-05-21.csv'
                                ),
                            },
                        },
                        {
                            'run': 'dataframe.select.columns@v1',
                            'params': {
                                'select': {
                                    "timestamp": "timestamp",
                                    "sample-downstream": "temperature2",
                                }
                            },
                        },
                        {
                            'run': 'dataframe.setindex@v1',
                            'params': {
                                'index_var': 'timestamp',
                            },
                        },
                    ],
                },
            },
        ]

        # create workflow
        workflow = Workflow.create(descriptor)
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16
        assert len(df.columns) == 7

    def test_create_with_single_process_instance(self, data_path):
        # create workflow
        workflow = Workflow.create(loaders.MksFTIRLoader())
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_create_with_single_process_name(self, data_path):
        # create workflow
        workflow = Workflow.create('mks.ftir@v1')
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_create_with_single_process_instance_and_params_dict(self, data_path):
        # create workflow
        workflow = Workflow.create(
            (
                loaders.MksFTIRLoader(),
                dict(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn')),
            )
        )
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_create_with_single_process_name_and_params_dict(self, data_path):
        # create workflow
        workflow = Workflow.create(
            (
                'mks.ftir@v1',
                dict(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn')),
            )
        )
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 16

    def test_create_with_sequence_of_process_instance(self, data_path):
        # create workflow
        workflow = Workflow.create(
            [
                loaders.MksFTIRLoader(),
                (
                    'dataframe.select.timespan@v1',
                    dict(
                        column='timestamp',
                        start='2024-01-16T10:05:22.5',
                        stop='2024-01-16T10:05:27.5',
                    ),
                ),
                (
                    'dataframe.select.columns@v1',
                    dict(
                        select={
                            "timestamp": "timestamp",
                            "NH3 (3000) 191C (2of2)": "NH3",
                            "N2O (100,200,300) 191C (1of2)": "N2O",
                            "NO (350,3000) 191C": "NO",
                            "NO2 (2000) 191C (2of2)": "NO2",
                            "NO2 (150) 191C (1of2)": "NO2b",
                            "H2O% (25) 191C": "H2O",
                        }
                    ),
                ),
            ]
        )
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run(source=str(data_path / 'mks_ftir/2024-01-16-conc.prn'))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 7

    def test_create_with_sequence_of_process_instance_and_executable_parameter(
        self, data_path
    ):
        # create workflow
        workflow = Workflow.create(
            [
                (
                    'dataframe.select.timespan@v1',
                    {
                        '$source': (
                            loaders.MksFTIRLoader(),
                            dict(
                                source=str(data_path / 'mks_ftir/2024-01-16-conc.prn')
                            ),
                        ),
                        'column': 'timestamp',
                        'start': '2024-01-16T10:05:22.5',
                        'stop': '2024-01-16T10:05:27.5',
                    },
                ),
                (
                    'dataframe.select.columns@v1',
                    dict(
                        select={
                            "timestamp": "timestamp",
                            "NH3 (3000) 191C (2of2)": "NH3",
                            "N2O (100,200,300) 191C (1of2)": "N2O",
                            "NO (350,3000) 191C": "NO",
                            "NO2 (2000) 191C (2of2)": "NO2",
                            "NO2 (150) 191C (1of2)": "NO2b",
                            "H2O% (25) 191C": "H2O",
                        }
                    ),
                ),
            ]
        )
        assert isinstance(workflow, Workflow)

        # run workflow
        df = workflow.run()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 7
