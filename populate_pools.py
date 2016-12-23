# Connect users to another another to test (twitter)

from integrations.models.twitter import TwitterPerson

k = TwitterPerson.objects.get(username='katyperry')
o = TwitterPerson.objects.get(username='BarackObama')
j = TwitterPerson.objects.get(username='justinbieber')

k.pool.add(o)
k.pool.add(j)
k.save()

o.pool.add(k)
o.save()

j.pool.add(k)
j.save()
