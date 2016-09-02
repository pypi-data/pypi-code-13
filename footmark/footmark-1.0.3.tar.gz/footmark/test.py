import footmark
import footmark.ecs as ecs_mo
def main():
    try:
        # params = dict(acs_access_key_id='6Klry3WV1KkUR4wH', acs_secret_access_key='anVR23gUHVTlOU0XKevVmYCog2tH0M')
        # region_id = 'cn-qingdao'
        # instance_ids = ["i-28uhiz4lq"]
        params = dict(acs_access_key_id='Q1QzBSnuozXv7y98', acs_secret_access_key='4g4QQ6cBtyN3D7DjghtHOKm8ygRkZD')
        region_id='cn-shenzhen'

        conn = ecs_mo.connect_to_region(region_id, **params)
        instance_ids=["i-94dehop6n"]
        filters = {}
        tag_key = 'xz_test'
        tag_value = '1.20'
        filters['tag:'+tag_key] = tag_value
        filters['instance_ids'] = instance_ids
        result = conn.get_all_instances(instance_ids=None, filters = filters)
        # print 'test result: ',vars(result[0])
        # print 'vpc_attribute: ', result[0].vpc_attributes
        # print 'inner_ip: ', result[0].inner_ip_address
        # print 'eip_attr: ', result[0].eip_address
        # print 'vpc_id: ', result[0].vpc_id
        # print 'vswitch_id: ', result[0].vswitch_id
        # print 'private_ip: ', result[0].private_ip
        # print 'Instance_id', result[0].instance_id
        print 'connet', result[0].status
        # for inst in result:
        for inst in result:
            if inst.status == 'Stopped':
                inst.start()
            if inst.status == 'Running':
                inst.stop()
            print 'status:', inst.state
    except:
        raise

main()