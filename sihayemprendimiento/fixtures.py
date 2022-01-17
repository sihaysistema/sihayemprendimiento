# -*- coding: utf-8 -*-
#  Si Hay Sistema and Contributors 2022

from __future__ import unicode_literals


def fill_fixtures():
    # We declare fixtures as an empty list.
    fixtures_fillup = []

    # Add the corresponding fields to the fixture objects
    # if the object does not exist, simply create it and copy accordingly.

    # custom_field = {
    #     "dt": "Custom Field", "filters": [
    #         [
    #             "name", "in", []
    #         ]
    #     ]
    # }

    translation = {
        "dt": "Translation", "filters": [
            [
                "source_text", "in", [
                    "Data Sent", "Data Received", "Records", "Total Due",
                    "Posting Date Time", "SHS Data Received", "SHE Data Sent",
                    "Receiver?", "Product To Be Invoiced", "Sales Taxes and Charges Default"
                ]
            ]
        ]
    }

    # fixtures_fillup.append(custom_field)
    fixtures_fillup.append(translation)

    return fixtures_fillup
