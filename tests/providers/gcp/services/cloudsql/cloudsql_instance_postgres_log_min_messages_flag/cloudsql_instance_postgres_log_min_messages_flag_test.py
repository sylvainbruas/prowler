from unittest import mock

from tests.providers.gcp.gcp_fixtures import (
    GCP_EU1_LOCATION,
    GCP_PROJECT_ID,
    set_mocked_gcp_provider,
)


class Test_cloudsql_instance_postgres_log_min_messages_flag:
    def test_no_cloudsql_instances(self):
        cloudsql_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_client",
                new=cloudsql_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag import (
                cloudsql_instance_postgres_log_min_messages_flag,
            )

            cloudsql_client.instances = []

            check = cloudsql_instance_postgres_log_min_messages_flag()
            result = check.execute()
            assert len(result) == 0

    def test_cloudsql_mysql_instance(self):
        cloudsql_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_client",
                new=cloudsql_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag import (
                cloudsql_instance_postgres_log_min_messages_flag,
            )
            from prowler.providers.gcp.services.cloudsql.cloudsql_service import (
                Instance,
            )

            cloudsql_client.instances = [
                Instance(
                    name="instance1",
                    version="MYSQL_5_7",
                    ip_addresses=[],
                    region=GCP_EU1_LOCATION,
                    public_ip=False,
                    require_ssl=False,
                    ssl_mode="ENCRYPTED_ONLY",
                    automated_backups=True,
                    authorized_networks=[],
                    flags=[],
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudsql_instance_postgres_log_min_messages_flag()
            result = check.execute()
            assert len(result) == 0

    def test_cloudsql_instance_no_flags(self):
        cloudsql_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_client",
                new=cloudsql_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag import (
                cloudsql_instance_postgres_log_min_messages_flag,
            )
            from prowler.providers.gcp.services.cloudsql.cloudsql_service import (
                Instance,
            )

            cloudsql_client.instances = [
                Instance(
                    name="instance1",
                    version="POSTGRES_15",
                    ip_addresses=[],
                    region=GCP_EU1_LOCATION,
                    public_ip=False,
                    require_ssl=False,
                    ssl_mode="ENCRYPTED_ONLY",
                    automated_backups=True,
                    authorized_networks=[],
                    flags=[],
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudsql_instance_postgres_log_min_messages_flag()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "PostgreSQL Instance instance1 does not have 'log_min_messages' flag set."
            )
            assert result[0].resource_id == "instance1"
            assert result[0].resource_name == "instance1"
            assert result[0].location == GCP_EU1_LOCATION
            assert result[0].project_id == GCP_PROJECT_ID

    def test_cloudsql_instance_log_min_messages_flag_off(self):
        cloudsql_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_client",
                new=cloudsql_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag import (
                cloudsql_instance_postgres_log_min_messages_flag,
            )
            from prowler.providers.gcp.services.cloudsql.cloudsql_service import (
                Instance,
            )

            cloudsql_client.instances = [
                Instance(
                    name="instance1",
                    version="POSTGRES_15",
                    ip_addresses=[],
                    region=GCP_EU1_LOCATION,
                    public_ip=False,
                    require_ssl=False,
                    ssl_mode="ENCRYPTED_ONLY",
                    automated_backups=True,
                    authorized_networks=[],
                    flags=[{"name": "log_min_messages", "value": "debug1"}],
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudsql_instance_postgres_log_min_messages_flag()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "PostgreSQL Instance instance1 has 'log_min_messages' flag set to 'DEBUG1', which is below the recommended minimum of 'ERROR'."
            )
            assert result[0].resource_id == "instance1"
            assert result[0].resource_name == "instance1"
            assert result[0].location == GCP_EU1_LOCATION
            assert result[0].project_id == GCP_PROJECT_ID

    def test_cloudsql_instance_log_min_messages_flag_on(self):
        cloudsql_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_client",
                new=cloudsql_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudsql.cloudsql_instance_postgres_log_min_messages_flag.cloudsql_instance_postgres_log_min_messages_flag import (
                cloudsql_instance_postgres_log_min_messages_flag,
            )
            from prowler.providers.gcp.services.cloudsql.cloudsql_service import (
                Instance,
            )

            cloudsql_client.instances = [
                Instance(
                    name="instance1",
                    version="POSTGRES_15",
                    ip_addresses=[],
                    region=GCP_EU1_LOCATION,
                    public_ip=False,
                    require_ssl=False,
                    ssl_mode="ENCRYPTED_ONLY",
                    automated_backups=True,
                    authorized_networks=[],
                    flags=[{"name": "log_min_messages", "value": "error"}],
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudsql_instance_postgres_log_min_messages_flag()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "PostgreSQL Instance instance1 has 'log_min_messages' flag set to an acceptable severity level: 'ERROR'."
            )
            assert result[0].resource_id == "instance1"
            assert result[0].resource_name == "instance1"
            assert result[0].location == GCP_EU1_LOCATION
            assert result[0].project_id == GCP_PROJECT_ID
