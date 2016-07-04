from redis_s3_backup import backup
import argparse

def main():
    """Parse command-line arguments and pass them to backup()"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Directory in which dump.rdb is located")
    parser.add_argument("--bucket", help="S3 bucket to be used to store backups")
    parser.add_argument("--profile", help="AWS profile to be used when loading credentials")
    args = parser.parse_args()
    backup(args.directory, args.bucket, args.profile)

if __name__ == '__main__':
    main()
