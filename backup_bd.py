import os
import argparse
import subprocess

def get_args():
    parser = argparse.ArgumentParser(description='Script for creating backups')
    parser.add_argument('-u', '--user', type=str, help='DB login')
    parser.add_argument('-p', '--password', type=str, help='DB password')
    parser.add_argument('-b', '--base', type=str, help='DB name')
    parser.add_argument('-d', '--directory', type=str, help='Backup directory')
    parser.add_argument('-h', '--host', type=str, help='DB location')
    parser.add_argument('-pr', '--prefix', type=str, help='Root of the CRM')
    return parser.parse_args()

def make_dump(dbuser, dbpass, dblocation, dbname, backupdir):
    now = os.popen('date +"%d%m%Y"').read().strip()
    hostname = os.popen("awk -F '.' '{print $1}' /etc/hostname").read().strip()

    size_command = "mysql -h {} -u {} -p{} --silent --skip-column-names -e \"SELECT ROUND(SUM(data_length) / 1024 / 1024 ,0) FROM information_schema.TABLES WHERE table_schema='{}';\"".format(dblocation, dbuser, dbpass, dbname)
    size = int(os.popen(size_command).read().strip())

    dump_command = "mysqldump -h {} -u {} -p{} {} --single-transaction --ignore-table='{}.mivio_log' --ignore-table='{}.fiscalreg_atol_tasks' --ignore-table='{}.cbase_log' | gzip > {}.{}.{}.sql.gz".format(
        dblocation, dbuser, dbpass, dbname, dbname, dbname, dbname, hostname, dbname, now
    )
    subprocess.run(['bash', '-c', dump_command])

    mv_command = "sudo mv {}.{}.{}.sql.gz {}/{}.{}.{}.sql.gz".format(
        hostname, dbname, now, backupdir, hostname, dbname, now
    )
    subprocess.run(['bash', '-c', mv_command])


if __name__ == '__main__':
    args = get_args()
    dbuser = args.user if args.user else ""
    dbpass = args.password if args.password else ""
    dblocation = args.host if args.host else "localhost"
    dbname = args.base if args.base else ""
    prefix = args.prefix if args.prefix else "/var/www/html"
    backupdir = args.directory if args.directory else prefix + "/backup"
    make_dump(dbuser, dbpass, dblocation, dbname, backupdir)
