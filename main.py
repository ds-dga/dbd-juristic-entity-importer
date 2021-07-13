from ckan import push2ckan
import toml
from dbd import get_dbd_csv, process_dbd_csv


def get_toml_config():
    with open("settings.toml", "rt") as f:
        parsed_toml = toml.loads(f.read())
        print(parsed_toml)
        return parsed_toml


def main():
    conf = get_toml_config()
    for k, v in conf["source"].items():
        if k.find("dbd") > -1:
            # fetch all csv to DATA_DIR
            get_dbd_csv(v['url'])
            records = process_dbd_csv()
            print(f"RECORD: {k}")
            for k2, v2 in records.items():
                print(f"   {k2}      {len(v2):7d}")
            push2ckan(v, records, conf['ckan'])
            continue
        print(f"{k} is not supported.")


if __name__ == "__main__":
    main()
