#!/bin/bash
ssh -i /ssh/id_rsa -o StrictHostKeyChecking=no -p 2222 -R dash:80:localhost:10810 lt.bend.ovh
