import itertools

from tldextract import extract
from tqdm import tqdm

from config import *
from utils.struct import *
from utils.utils import *


def feature(data):
    return data


def preprogress(data_path):
    global label_set, website_list
    print('Start progress packets...')
    file_list = os.listdir(data_path)
    url_list = list(map(lambda x: x.replace('___', '://', 1).replace('_', '/'), file_list))
    website_list = list(map(lambda x: extract(x).domain, url_list))
    label_set = get_label_set(website_list)
    tls_instances = get_tls_instances(data_path, file_list)
    feature = get_features(tls_instances)
    return feature


@middle(file=temp_path + 'tls_instances.tmp')
def get_tls_instances(data_path, file_list):
    return [get_tls_instance(open(os.path.join(data_path, file)).read()) for file in tqdm(file_list)]


@middle(file=temp_path + 'label_set.bin')
def get_label_set(domain_list):
    return list(set(domain_list))


@middle(file=temp_path + 'feature.bin')
def get_features(tls_instances):
    print('Start extract feature...')
    return [get_feature(instance, index) for index, instance in enumerate(tqdm(tls_instances))]


def get_tls_instance(text):
    instance_lines = filter(lambda x: len(x) > 0, text.rstrip().split('\n'))
    instances = []
    for trace in instance_lines:
        trace = trace.rstrip().split(' ')
        url, timestamp, *_ = trace
        if len(timestamp) > 13:
            timestamp = timestamp[:13]
        if ':' in trace[2]:
            entrynodes = '0'
            data = trace[2:]
        else:
            entrynodes = trace[2]
            data = trace[3:]

        packets = []
        for entry in data:
            # for compatibility
            if len(entry.split(':')) == 3:
                packet = Packet(entry.split(':')[1], entry.split(':')[2])
            elif len(entry.split(':')) == 2:
                packet = Packet('', entry.split(':')[1])
            else:
                print("ERROR: Unkown instance format!")
                packet = Packet('', '')
            packets.append(packet)
        instances.append(Instance(url, timestamp, entrynodes, packets))
        instances.sort(key=lambda x: x.incoming_size)
    return instances


def get_feature(instance, instance_index):
    classLabel = label_set.index(website_list[instance_index])
    features = []
    total = []
    cum = []
    pos = []
    neg = []
    inSize = 0
    outSize = 0
    inCount = 0
    outCount = 0

    # Process trace
    for item in itertools.islice(instance.packets):
        packetsize = int(item.packetsize)

        # incoming packets
        if packetsize > 0:
            inSize += packetsize
            inCount += 1
            # cumulated packetsizes
            if len(cum) == 0:
                cum.append(packetsize)
                total.append(packetsize)
                pos.append(packetsize)
                neg.append(0)
            else:
                cum.append(cum[-1] + packetsize)
                total.append(total[-1] + abs(packetsize))
                pos.append(pos[-1] + packetsize)
                neg.append(neg[-1] + 0)

        # outgoing packets
        if packetsize < 0:
            outSize += abs(packetsize)
            outCount += 1
            if len(cum) == 0:
                cum.append(packetsize)
                total.append(abs(packetsize))
                pos.append(0)
                neg.append(abs(packetsize))
            else:
                cum.append(cum[-1] + packetsize)
                total.append(total[-1] + abs(packetsize))
                pos.append(pos[-1] + 0)
                neg.append(neg[-1] + abs(packetsize))

    # add feature
    features.append(classLabel)
    features.append(inCount)
    features.append(outCount)
    features.append(outSize)
    features.append(inSize)
