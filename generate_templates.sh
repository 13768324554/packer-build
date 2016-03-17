#!/usr/bin/env bash

for template in $(find {debian,ubuntu} -name '*.yaml'); do
    if [ ! -f "${template}" ]; then continue; fi
    echo "Generating ${template/yaml/json}"
    ./yaml2json.rb < "${template}" > "${template/yaml/json}"
    packer fix "${template/yaml/json}" > "${template/yaml/json}.new"
    mv "${template/yaml/json}.new" "${template/yaml/json}"
done
