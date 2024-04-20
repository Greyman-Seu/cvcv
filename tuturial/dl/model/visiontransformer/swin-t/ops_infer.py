import torch
from fvcore.nn import FlopCountAnalysis
from swin_transformer import swin_small_patch4_window7_224
from swin_transformer_v2 import swin_small_patch4_window7_224 as swin_small_patch4_window7_224_v2


def tiny_model_infer():
    model = swin_small_patch4_window7_224()
    
    bs=2
    img_size = 224
    fake_img = torch.rand(bs,3,img_size,img_size) # BCHW
    
    # infer
    print(model(fake_img))
    
    # op
    fca = FlopCountAnalysis(model,(fake_img,))
    print("flops total: ", fca.total())
    print("   by_operator: ", fca.by_operator())
    #print("   by_module: ", fca.by_module())
    #print("   by_module_and_operator: ", fca.by_module_and_operator())
    
def tiny_modelv2_infer():
    model = swin_small_patch4_window7_224_v2()
    
    bs=2
    img_size = 224
    fake_img = torch.rand(bs,3,img_size,img_size) # BCHW
    
    # infer
    print(model(fake_img))
    
    # op
    fca = FlopCountAnalysis(model,(fake_img,))
    print("flops total: ", fca.total())
    print("   by_operator: ", fca.by_operator())
    #print("   by_module: ", fca.by_module())
    #print("   by_module_and_operator: ", fca.by_module_and_operator())
    
    
def main():
    tiny_model_infer()
    tiny_modelv2_infer()

    
if __name__ == '__main__':
    main()