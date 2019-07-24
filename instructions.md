### **First of all, please let me know if you need to modify any script in our project directory.**

## Spin up Emulab machines
The first step to run SVCOMP benchmarks is to spin up emulab machines. In our Emulab group, experiments `SMACKBench-SMACKBench22` are created and used to run SVCOMP benchmarks. Each experiment contains one node (machine). We usually use d820 nodes and occasionally use d430 nodes. The reason is that each benchmark requires 15GB memory. A d820 node and d430 node has 120GB and 64GB memory respectively, which means that we can run 8 benchmarks in parallel on a d820 node while only 4 on a d430 node. `SMACKBench-SMACKBench4` are configured to use d820 nodes by default. We cannot allocate more than 4 d820 nodes per Emulab’s restriction. Click on `Swap Experiment In` on the experiment’s webpage to spin up a node (e.g., https://www.emulab.net/showexp.php3?pid=SMACK&eid=SMACKBench).

After a machine is swapped in, the script `/proj/SMACK/scripts/smackbench_compute_repo_buildscript.sh` will run automatically to install our SVCOMP benchmarking infrastructure as well as SMACK and its dependencies. By default, the develop branch of SMACK is cloned under `/mnt/local/smack-project`. If you need to change SMACK, modify this folder and reinstall SMACK by executing command `sudo bin/build.sh` under `/mnt/local/smack-project/smack` (remember to modify `build.sh` since we only need to build and install SMACK while it by default does everything). The output of the build script is redirected to `/tmp/smackbench_compute_build.out`. You can invoke command `tail -f /tmp/smackbench_compute_build.out` to check the installation status. **The machine will reboot after the build script finishes.** 

## Run SMACKBench.py
After the machine reboots, we are good to run SVCOMP benchmarks. The python script to run them is `SMACKBench.py` which is in the folder `/proj/SMACK/SMACKBenchResults`. It contains two modes `server` and `run`. The former runs all the SVCOMP benchmarks and the latter runs a single category.

### Run all the categories
The server mode maintains a queue file that specifies the category and the configuration it requires. There is a template of such queue in `/proj/SMACK/SMACKBenchResults/inputFiles` called `queueStdBuiltNew`. Its content is the following,

```
MemSafety-Arrays inputFiles/inputXMLFiles/svcomp_m32_witcheck.xml
ReachSafety-Arrays inputFiles/inputXMLFiles/svcomp_m32_witcheck.xml
Overflows-BitVectors inputFiles/inputXMLFiles/svcomp_m64_witcheck.xml
…
```
The left column specifies the category and the right column specifies the configuration file for that category. **Please do not modify these configuration files. If you do need to run a new configuration, create one and update the column in the queue file.**

You can get help information of the server mode by executing `./SMACKBench.py server -h`. The following is an example to run server mode,

``` bash
$ source /mnt/local/smack-project/smack.environment
$ cd /proj/SMACK/SMACKBenchResults
$ cd inputFiles
$ cp queueStdBuiltNew queue1
$ cd ..
$ ./SMACKBench.py server -q inputFiles/queue1 -d develop-1234567-first-run
```

You need to create a queue file first by copying the template `queueStdBuiltNew` to a file (`queue1` in this example). You don not need to touch other flags other than `-d` if the node is of type d820. The string after `-d` will be a descriptor for this run. We do have an informal naming convention for the descriptors: `<branch>-<7 digit commit id>-<additional info>`. For this example, `develop` is the branch name, `1234567` is the commit, `first-run` is the additional information. **Try to come up with a unique descriptor for each run. It will help us to compare the results between two different runs.**

The server mode of SMACKBench.py runs as python daemons and the result will be redirected to a file whose name will show up after SMACKBench.py is invoked. Again, you can peek its content by using the command `tail -f`. Meanwhile, you can also check the status on http://node0.smackbenchwebserver.smack.emulab.net/, which may not be up-to-date because the benchmarking tool only flushes the buffer after it is full and after that the website will reflect the results.

**To stop the server mode, run the command** `./SMACKBench.py stop`.

### Run a single category
The run mode of SMACKBench is similar to the server mode. You can also see the help inforomation by executing `./SMACKBench.py run -h`. The differences would be that you have to choose the set name and the configuration (inputXML) file of the category that you would like to run. Please refer to the template queue file to find out what is the set name and its associated inputXML file. The following is an example of the run mode,

```bash
$ cd /proj/SMACK/SMACKBenchResults
$ ./SMACKBench.py run -s ReachSafety-Arrays -x inputFiles/inputXMLFiles/svcomp_m32_witcheck.xml -d develop-1234567-first-run
```
The output of `SMACKBench.py` in run mode will not be redirected to a special file. Instead it will be printed to the standard output. Moreover, running `./SMACKBench.py stop` may not stop the run mode.

## Clean up temporary files
Running SVCOMP benchmarks will create tons of temporary files which will eat up our project disk quota after several runs. Therefore, make sure to run the clean up script after each run. To clean up, run the following command,

```bash
cd /proj/SMACK/SMACKBenchResults/data && ./clean.sh
```

## Remove old runs
If any old runs are no long needed, please remove them as soon as possible for two reasons. First, we have a project disk quota. Second, the new results are easier to track since all runs are shown in the result webpage. To erase a run, simply remove the corresponding subfolders in the directory `/proj/SMACK/SMACKBenchResults/data/runs`. All the subfolders in this directory are named in the following way: `exec_<date>_<setname>` (e.g., `exec_2017.06.23_23.54.36.506827_ReachSafety-ECA`), where `<date>` can be found in the result webpage.

To remove all the folders belonging to a run that has a **unique** descriptor, you can refer to the following commands that I usually use. For example,
```bash
cd /proj/SMACK/SMACKBenchResults/data/runs
for f in `find . -mindepth 3 -maxdepth 3 -name "*<run-id>*.xml"`; do a=`dirname $f`; b=`dirname $a`; echo $b; done | xargs -n 1 -P 32 rm -r
```
`<run-id>` is the unique descriptor of the run that you want to remove. Please double check if the wildcard expands to more files than what you are intereted in.
