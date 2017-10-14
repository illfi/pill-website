import subprocess
import os

pill = '/Users/haze/Projects/Rust/pill/target/release/pill' # yeah, my filesystem is organized... is yours??!!!

def get_output(program_name):
    return subprocess.check_output([pill, "-q", program_name])
for ex in [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]:
    o = os.path.join(os.getcwd(), ex, '{}_output.txt'.format(ex))
    f = os.path.join(os.getcwd(), ex, '{}.ill'.format(ex))
    with open(o, 'w+') as z:
        z.write(get_output(f).decode('utf-8'))