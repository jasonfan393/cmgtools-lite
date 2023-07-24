import json
all=json.loads(open("btagging_2018_UL.json").read())
corr=all['corrections']
blah=None
for what in corr:
    if what['name']=='deepJet_shape':
        deepjet=what

systematic = deepjet['data']['content']
for k in systematic:
    if k['key'] == 'central':
        node=k['value']

for flavor in node['content']:
    if flavor['key'] == 0:
        light=flavor['value']

eta=light['content'][1] # picking eta between 0.8 and 1.6
print(eta['edges'])
pt = eta['content'][3] # picking pt between 60 and 100 
print(pt['edges'])
print(pt['content'][0]) # picking discriminator between 0.0 and 0.01


