import yaml

def search_dict_list(a_val, b_val, c_list):
    for line in c_list:
        if line['hostname'] == a_val:
            return line[b_val]

# Define Variables

num_spines = 2
num_leafs = 8
p2p_range = '10.0.'
lo0_range = '10.0.250.'
lo1_range = '10.0.255.'
ibgp_range = '10.0.3.'
ibgp_vlan = '4091'
asn_start = 65000

# Generate host_vars for Leafs

leaf_list = []
asn = asn_start+1
n = 0
for i in range(num_leafs):
    id = i+1
    device = {}
    device['interfaces'] = []
    device['bgp_neighbors'] = []
    device['evpn_neighbors'] = []
    device['hostname'] = f'leaf{id}'
    device['loopback0_ip'] = f'{lo0_range}{id+10}'
    device['loopback1_ip'] = f'{lo1_range}{id+10}'
    if id%2 == 1:
        device['side'] = 'left'
        device['asn'] = asn
        asn +=1
        device['bgp_neighbors'].append({'neighbor':f'{ibgp_range}{id}', 'remote_as': device['asn'], 'state': 'present'})
    else:
        device['side'] = 'right'
        device['asn'] = asn-1
        device['bgp_neighbors'].append({'neighbor':f'{ibgp_range}{id-2}', 'remote_as': device['asn'], 'state': 'present'})
    for j in range(num_spines):
        device['interfaces'].append({'interface':f'Ethernet{j+11}', 'address':f'{p2p_range}{j+1}.{n+1}', 'mask':'/31', 'description':f'spine{j+1}'})
        device['bgp_neighbors'].append({'neighbor':f'{p2p_range}{j+1}.{n}', 'remote_as': asn_start, 'state': 'present'})
        device['evpn_neighbors'].append({'neighbor':f'{lo0_range}{j+1}', 'remote_as': asn_start, 'state': 'present'})
    device['interfaces'].append({'interface': f'Vlan{ibgp_vlan}', 'address':f'{ibgp_range}{i}', 'mask':'/31'})
    leaf_list.append(device)
    n+=2

    outputfile = './host_vars/{}.yaml'.format(device['hostname'])
    f = open(outputfile, 'w')
    yaml.dump(device, f, default_flow_style=False)

# Generate host_vars for Spines

spine_list = []
asn = asn_start
for i in range(num_spines):
    id = i+1
    device = {}
    device['interfaces'] = []
    device['bgp_neighbors'] = []
    device['evpn_neighbors'] = []
    device['hostname'] = f'spine{id}'
    device['loopback0_ip'] = f'{lo0_range}{id}'
    device['asn'] = asn
    n = 0
    for j in range(num_leafs):
        leaf_asn = search_dict_list(f'leaf{j+1}','asn',leaf_list)
        device['interfaces'].append({'interface':f'Ethernet{j+1}', 'address':f'{p2p_range}{id}.{n}', 'mask':'/31', 'description':f'leaf{j+1}'})
        device['bgp_neighbors'].append({'neighbor':f'{p2p_range}{id}.{n+1}', 'remote_as': leaf_asn, 'state': 'present'})
        device['evpn_neighbors'].append({'neighbor':f'{lo0_range}{j+11}', 'remote_as': leaf_asn, 'state': 'present'})
        n += 2

    outputfile = './host_vars/{}.yaml'.format(device['hostname'])
    f = open(outputfile, 'w')
    yaml.dump(device, f, default_flow_style=False)

#print(yaml.dump(leaf_list))
#print(yaml.dump(spine_list))
