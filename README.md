# Ansible Lab to Deploy EVPN on Arista vEOS fabric

Referenced in a blog post on overlaid.net (https://overlaid.net/2019/02/19/arista-bgp-evpn-ansible-lab/)

The following Playbooks are included:

- generate_host_vars.yml - Generates the host variables used in Ansible (assuming 8 leafs, 2 spines)
- deploy_evpn.yml - Deploys the EVPN Lab
- validate_lab.yml - Validates the Lab after deploying EVPN (LLDP, MLAG, BGP, EVPN)
- deploy_l2vxlan.yml - Deploys a L2 VXLAN Service. Requires you to pass in a VLAN name and VLAN ID
- deploy_l3vxlan.yml - Deploys a L3 VXLAN Service. Requires you to pass in a VRF name and VRF ID

Still lots of work to be done, features to add, and optimizations to make. This is V1.
