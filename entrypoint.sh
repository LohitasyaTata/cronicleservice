#!/bin/bash


unzip -o /home/bflmfuser/code.zip -d /home/bflmfuser
# source /home/bflmfuser/venv/bin/activate
for line in $(cat /home/bflmfuser/amccore/app/requirements.txt)
  do 
          pip install --no-index  $line --find-links=/home/bflmfuser/python_packages

          if (( $? == 0 )); then
                  echo 'command was successful'
          else
                  echo 'damn, there was an error'
                  echo $line >> exception.txt
          fi
  done

# export ENVIRONMENT=DEV
# export service_name=amc_cronical_service
# export configuration_service_url=http://configurationservice.dev.bfsgodirect.com
chmod 777 /home/bflmfuser/amccore/ -R
chmod 777 -R /home/bflmfuser/venv/bin/python
chmod 777 /home/bflmfuser/amccore/app/mf_init.sh
cd /home/bflmfuser/amccore/app/ && ./mf_init.sh > /mf_init_out.log




ROOT_DIR=/opt/cronicle
CONF_DIR=$ROOT_DIR/conf
BIN_DIR=$ROOT_DIR/bin
# DATA_DIR needs to be the same as the exposed Docker volume in Dockerfile
DATA_DIR=$ROOT_DIR/data
# LOGS_DIR needs to be the same as the exposed Docker volume in Dockerfile
LOGS_DIR=$ROOT_DIR/logs
# PLUGINS_DIR needs to be the same as the exposed Docker volume in Dockerfile
PLUGINS_DIR=$ROOT_DIR/plugins

# The env variables below are needed for Docker and cannot be overwritten
# export CRONICLE_Storage__Filesystem__base_dir=${DATA_DIR}
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
export CRONICLE_echo=1
export CRONICLE_foreground=1
nvm list-remote
node -v
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

/opt/cronicle/bin/control.sh setup
# Only run setup when setup needs to be done
# if [ ! -f $DATA_DIR/.setup_done ]
# then
  
#   echo "Node Version "
#   node -v

#   $BIN_DIR/control.sh setup

#   cp $CONF_DIR/config.json $CONF_DIR/config.json.origin

#   if [ -f $DATA_DIR/config.json.import ]
#   then
#     # Move in custom configuration
#     cp $DATA_DIR/config.json.import $CONF_DIR/config.json
#   fi

#   # Create plugins directory
#   mkdir -p $PLUGINS_DIR

#   # Marking setup done
#   touch $DATA_DIR/.setup_done
# fi

# Run cronicle with unprivileged user
# chown -R cronicle:cronicle data/ logs/

# remove old lock file. resolves #9
PID_FILE=$LOGS_DIR/cronicled.pid
if [ -f "$PID_FILE" ]; then
    echo "Removing old PID file: $PID_FILE"
    rm -f $PID_FILE
fi

if [ -n "$1" ];
then
#   if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
#     set -- cronicle "$@"
#   fi
  exec "$@"
else
#   exec su cronicle -c "/opt/cronicle/bin/control.sh start"

    /opt/cronicle/bin/control.sh start
fi
#sh ~/.bashrc && nvm use v16.2.0 && /opt/cronicle/bin/control.sh start