#!/usr/bin/env python3
"""
Safe XML-RPC connection test script for Odoo.
Uses environment variables for credentials and performs
an optimized search_read query with explicit fields.

Author: CTiEG (hola@ctieg.com | www.ctieg.com)
License: MIT
"""

import os
import sys
import logging
from xmlrpc.client import ServerProxy, Fault

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("odoo_xmlrpc_test")


def load_env_or_exit(var_name: str) -> str:
    """Load an environment variable or exit with error."""
    value = os.getenv(var_name)
    if not value:
        logger.error(
            "Environment variable %s not set. "
            "Export it before running the script:\n"
            "  export %s=\"value\"",
            var_name,
            var_name,
        )
        sys.exit(1)
    return value


def test_odoo_connection() -> None:
    """
    Test the XML-RPC connection to Odoo using credentials
    from environment variables and execute a search_read query
    on the res.partner model.
    """
    odoo_url = load_env_or_exit("ODOO_URL")
    odoo_db = load_env_or_exit("ODOO_DB")
    odoo_user = load_env_or_exit("ODOO_USER")
    odoo_api_key = load_env_or_exit("ODOO_API_KEY")

    common_endpoint = f"{odoo_url}/xmlrpc/2/common"
    object_endpoint = f"{odoo_url}/xmlrpc/2/object"

    logger.info("Connecting to Odoo: %s", odoo_url)
    logger.info("Database: %s", odoo_db)
    logger.info("User: %s", odoo_user)

    try:
        common = ServerProxy(common_endpoint)
        version = common.version()
        logger.info(
            "Odoo server detected: %s (v%s)",
            version.get("server_version", "unknown"),
            version.get("server_version", "?"),
        )
    except Fault as e:
        logger.error("Error getting server version: %s", e)
        sys.exit(1)

    try:
        uid = common.authenticate(odoo_db, odoo_user, odoo_api_key, {})
        if not uid:
            logger.error(
                "Authentication failed. Verify your credentials "
                "(user and API Key)."
            )
            sys.exit(1)
        logger.info("Authentication successful. UID: %s", uid)
    except Fault as e:
        logger.error("Authentication error: %s", e)
        sys.exit(1)

    try:
        models = ServerProxy(object_endpoint)
        partners = models.execute_kw(
            odoo_db,
            uid,
            odoo_api_key,
            "res.partner",
            "search_read",
            [  # domain (filters)
                ["is_company", "=", True]
            ],
            {
                "fields": ["id", "name", "email", "phone"],
                "limit": 5,
            },
        )

        if not partners:
            logger.warning(
                "No records found in res.partner "
                "with the applied filters."
            )
        else:
            logger.info(
                "Records retrieved (res.partner): %d", len(partners)
            )
            for partner in partners:
                logger.info(
                    "  ID=%-5s | Name=%-30s | Email=%-30s | Phone=%s",
                    partner.get("id"),
                    partner.get("name", "")[:30],
                    partner.get("email", "")[:30] or "N/A",
                    partner.get("phone", "") or "N/A",
                )

        logger.info("XML-RPC connection test completed successfully.")

    except Fault as e:
        logger.error("Error in XML-RPC call: %s", e)
        sys.exit(1)
    except ConnectionError as e:
        logger.error("Connection error with server: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    logger.info("=== START: Odoo XML-RPC connection test ===")
    test_odoo_connection()
    logger.info("=== END: Odoo XML-RPC connection test ===")