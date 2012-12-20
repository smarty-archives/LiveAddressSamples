//
//  LiveAddress API Example, Objective-C
//
//  A simple GET request to verify a street address, and the JSON response is
//  printed to the console.
//  

#import <Foundation/Foundation.h>

int main(int argc, const char * argv[])
{

    @autoreleasepool {
        
        // Make sure to replace the values of the GET request with your own, including
        // the auth-id and auth-token from your account. (URL encoded!)
        
        NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"https://api.smartystreets.com/street-address?street=1109+9th&city=phoenix&state=arizona&zipcode=85007&auth-id=<URL-ENCODED-AUTH-ID>&auth-token=<URL-ENCODED-AUTH-TOKEN>"]];
        NSData *response = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
        NSString *get = [[NSString alloc] initWithData:response encoding:NSUTF8StringEncoding];
        NSLog(@"%@", get);
        
    }
    return 0;
}

