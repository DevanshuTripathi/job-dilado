from mailer import get_all_jobs
import json
import argparse
from lever import get_lever_jobs
from amazon import get_amazon_jobs
from greenhouse import get_greenhouse_jobs
from ashby import get_ashby_jobs
from atlassian import get_atlassian_jobs
from google import get_google_jobs
from amazon_service_jobs import get_amazon_service_jobs


def preview():
    parser = argparse.ArgumentParser(description="Preview ats wise")
    parser.add_argument("--lever", action="store_true", help="Fetch lever jobs")
    parser.add_argument(
        "--greenhouse", action="store_true", help="Fetch greenhouse jobs"
    )
    parser.add_argument("--amazon", action="store_true", help="Fetch amazon jobs")
    parser.add_argument("--ashby", action="store_true", help="Fetch ashby jobs")
    parser.add_argument("--atlassian", action="store_true", help="Fetch atlassian jobs")
    parser.add_argument("--google", action="store_true", help="Fetch google jobs")
    parser.add_argument("--amzs", action="store_true", help="Fetch amazon service jobs")

    args = parser.parse_args()

    if (
        args.lever
        or args.amazon
        or args.greenhouse
        or args.ashby
        or args.atlassian
        or args.google
        or args.amzs
    ):
        hope_for_nalle_people = []
        if args.lever:
            hope_for_nalle_people.extend(get_lever_jobs())
        if args.greenhouse:
            hope_for_nalle_people.extend(get_greenhouse_jobs())
        if args.amazon:
            hope_for_nalle_people.extend(get_amazon_jobs())
        if args.ashby:
            hope_for_nalle_people.extend(get_ashby_jobs())
        if args.atlassian:
            hope_for_nalle_people.extend(get_atlassian_jobs())
        if args.google:
            hope_for_nalle_people.extend(get_google_jobs())
        if args.amzs:
            hope_for_nalle_people.extend(get_amazon_service_jobs())
    else:
        hope_for_nalle_people = get_all_jobs()

    jobs_dict = [job.model_dump() for job in hope_for_nalle_people]

    with open("preview.json", "w", encoding="utf-8") as file:
        json.dump(jobs_dict, file, indent=4)


if __name__ == "__main__":
    preview()
