import subprocess
import sys
import pickle

if __name__ == '__main__':
    """
    simple program to start and stop screen recording in obs
    @author https://mejuto.co @mejutoco
    example usage:
    - to start:
    python obs.py start "~/screencasts/"
    
    - to stop:
    python obs.py stop "~/screencasts/"
    """


    def get_current_git_commit():
        cmd = "git log -1 --oneline ".format(folder=folder)
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')
        current_hash = ret.strip().split(' ')[0].strip()
        return current_hash


    def get_last_git_message():
        """
        last commit message that is not 'TODO'
        we check for the last 30 only
        we take the first line of the commit (cannot be too long, since it will be in the file name)
        """
        cmd = "git log -30 --oneline | grep -v 'TODO' ".format(folder=folder)
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')
        lines = ret.split('\n')
        # remove the hash at the beginning
        # ex. "c28733cea let's make it effortless to record"
        tmp = lines[0].split(' ')[1:]
        commit_txt = " ".join(tmp)
        return commit_txt


    def save_start(start_file, obj):
        pickle.dump(obj, open(start_file, "wb"))


    def get_start(start_file):
        return pickle.load(open(start_file, "rb"))


    # here we will serialize the state while we are recording
    start_file = '~/obs_start.txt'

    action = sys.argv[1]
    folder = '.'
    if len(sys.argv) >= 3:
        folder = sys.argv[2]

    if action == 'start':
        start_commit = get_current_git_commit()

        obj = {
            'start_commit': start_commit,
        }
        save_start(start_file, obj)

        ret = subprocess.check_output(['obs', '--startrecording', '--minimize-to-tray'])
        print(ret)
    elif action == 'stop':
        # killing process stops obs
        try:
            cmd = "pkill obs"
            ret = subprocess.check_output(cmd, shell=True)
        except:
            # in case we stop manually we do not want this to break
            pass

        cmd = "ls {folder} -t | head -n1".format(folder=folder)
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')
        last_file = ret.strip()
        print(last_file)

        obj = get_start(start_file)
        end_commit = get_current_git_commit()
        title = get_last_git_message()
        print(folder, last_file, obj['start_commit'], end_commit, title)
        base_name = last_file.split('.mkv')[0]
        new_name = '{base_name}_{title}_{start}:{end}.mkv'.format(
            base_name=base_name,
            title=title,
            start=obj['start_commit'],
            end=end_commit,
        )
        new_name = new_name.replace(' ', '_')
        cmd = 'mv "{folder}/{last_file}" "{folder}/{new_name}"'.format(
            folder=folder,
            last_file=last_file,
            new_name=new_name,
        )
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # reset
        save_start(start_file, {})
        print(ret)
