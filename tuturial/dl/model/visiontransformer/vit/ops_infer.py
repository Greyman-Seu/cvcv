import torch
from fvcore.nn import FlopCountAnalysis
from model_vit import vit_tiny_patch16_224


def tiny_model_infer():
    model = vit_tiny_patch16_224()
    
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
    
    
def tiny_model_infer_dyn():
    # dynamic_img_size
    d_model = vit_tiny_patch16_224(dynamic_img_size=True)
    bs=2
    img_size = 512 # 可以不是224
    fake_img = torch.rand(bs,3,img_size,img_size) # BCHW
    
    # infer
    print(d_model(fake_img))
    
def main():
    # tiny_model_infer()
    tiny_model_infer_dyn()
    
if __name__ == '__main__':
    main()