#!/bin/bash

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -w|--workingdir)
    WORKINGDIR="$2"
    shift # past argument
    ;;
    -pv|--pvirtualenvdir)
    PVIRTUALENVDIR="$2"
    shift # past argument
    ;;
    -h|--help)
    echo "
	HELP:
	    -w: --workingdir: Project's base directory
	    -pv: --pvirtualenvdir: Python virtualenv directory
	" 
    shift # past argument
    ;;
esac
shift # past argument or value
done
if [ ! -z "${WORKINGDIR}" ]
then
echo WORKING DIR  = "${WORKINGDIR}"
echo PVIRTUALENVDIR = "${PVIRTUALENVDIR}"
source ${PVIRTUALENVDIR}/bin/activate
python ${WORKINGDIR}/abkayit/send_consent_email.py ${WORKINGDIR} 
else
echo !!!Some parameters missing!!!
echo "
      -w: --workingdir: Project's base directory
      -pv: --pvirtualenvdir: Python virtualenv directory"
fi
