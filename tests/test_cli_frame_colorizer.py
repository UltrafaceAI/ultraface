import subprocess
import sys
import pytest

from ultraface.download import conditional_download


@pytest.fixture(scope = 'module', autouse = True)
def before_all() -> None:
	conditional_download('.assets/examples',
	[
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/source.jpg',
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/target-240p.mp4'
	])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vframes', '1', '-vf', 'hue=s=0', '.assets/examples/target-240p-0sat.jpg' ])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vf', 'hue=s=0', '.assets/examples/target-240p-0sat.mp4' ])


def test_colorize_frame_to_image() -> None:
	commands = [ sys.executable, 'run.py', '--frame-processors', 'frame_colorizer', '-t', '.assets/examples/target-240p-0sat.jpg', '-o', '.assets/examples/test_colorize_frame_to_image.jpg', '--headless' ]
	run = subprocess.run(commands, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

	assert run.returncode == 0
	assert 'image succeed' in run.stdout.decode()


def test_colorize_frame_to_video() -> None:
	commands = [ sys.executable, 'run.py', '--frame-processors', 'frame_colorizer', '-t', '.assets/examples/target-240p-0sat.mp4', '-o', '.assets/examples/test_colorize_frame_to_video.mp4', '--trim-frame-end', '10', '--headless' ]
	run = subprocess.run(commands, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

	assert run.returncode == 0
	assert 'video succeed' in run.stdout.decode()
