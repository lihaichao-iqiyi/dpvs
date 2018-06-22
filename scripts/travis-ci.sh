#/bin/env sh

tester=115.182.224.11
sshport=8719

tarball="dpvs-ci.tar.bz2"

[ $# -ne 1 ] && echo -e "Usage: $0 build|deploy|test" && exit 1
case $1 in
build)
    tar -jcf $tarball ../dpvs
    scp -P $sshport $tarball ci@$tester:/home/ci
    ssh ci@$tester -p $sshport './travis-ci.sh build'
;;
deploy)
    ssh ci@$tester -p $sshport './travis-ci.sh deploy'
;;
test)
    ssh ci@$tester -p $sshport './travis-ci.sh test'
;;
*)
    echo -e "Usage: $0 build|deploy|test" && exit 1
;;
esac
